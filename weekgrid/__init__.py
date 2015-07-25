from django.db import models
from django import forms
from south.modelsinspector import add_introspection_rules

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

MORNING = (9, 13)
AFTERNOON = (13, 17)
EVENING = (17, 20)

slotlabels = {
    MORNING: "Morning",
    AFTERNOON: "Afternoon",
    EVENING: "Evening",
}

slottimes = {
    MORNING: "9AM - 1PM",
    AFTERNOON: "1PM - 5PM",
    EVENING: "5PM - 8PM",
}

daynames = {
    MONDAY: "Monday",
    TUESDAY: "Tuesday",
    WEDNESDAY: "Wednesday",
    THURSDAY: "Thursday",
    FRIDAY: "Friday",
    SATURDAY: "Saturday",
    SUNDAY: "Sunday",
}

shortdaynames = {
    MONDAY: "Mon",
    TUESDAY: "Tue",
    WEDNESDAY: "Wed",
    THURSDAY: "Thu",
    FRIDAY: "Fri",
    SATURDAY: "Sat",
    SUNDAY: "Sun",
}

class Weekgrid(dict):
    """A grid of true/false values for a set of time slots for each day of a week."""
    
    def __init__(self, slots=None, days=None):
        dict.__init__(self)
        
        # The time slots as a list of tuples (starthour, endhour)
        self._slots = slots
        if not self._slots:
            self._slots = [MORNING, AFTERNOON, EVENING]

        # The keys for which we store time slot data (ie. the days of the week)
        self._days = days
        if not self._days:
            self._days = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]

        # A dict-of-dicts holds the True/False data for each slot.
        for day in self._days:
            self[day] = {}
            for slot in self._slots:
                self[day][slot] = False

    def __and__(self, other):
        """Returns a weekgrid with slots set where both input weekgrids have slots set."""
        out = Weekgrid()

        for day in out._days:
            for slot in out._slots:
                out[day][slot] = self[day][slot] and other[day][slot]
        
        return out
    
    def __or__(self, other):
        """Returns a weekgrid with slots set if either input weekgrids have slots set."""
        out = Weekgrid()

        for day in out._days:
            for slot in out._slots:
                out[day][slot] = self[day][slot] or other[day][slot]
        
        return out
    
    def count(self):
        """Return the number of slots that are marked as available."""
        count = 0
        for day in self._days:
            for slot in self._slots:
                if self[day][slot]:
                    count += 1
        return count
    
    def to_list(self):
        data = []
        for slot in self._slots:
            for day in self._days:
                data.append(self[day][slot])
        return data
    
    def from_list(self, data):
        for slot in self._slots:
            for day in self._days:
                self[day][slot] = data.pop(0) if data else False
        return self

    def rendermini(self):
        return self.render(classes="pretty mini", short=True)

    def rendertiny(self, overlay=None):
        return self.render(classes="pretty tiny", short=True, overlay=overlay)

    def render(self, classes="pretty", short=False, overlay=None):
        out = "<table class='weekgrid_widget %s'><tr><th></th>" % classes
        for day in self._days:
            out += "<th>%s</th>" % (daynames[day] if not short else shortdaynames[day])
        out += "</tr>"

        for slot in self._slots:
            if short:
                out += "<tr><th class='slot'>%s</th>" % (slotlabels[slot])
            else:
                out += "<tr><th class='slot'>%s<div class='times'>(%s)</div></th>" % (slotlabels[slot], slottimes[slot])
                
            for day in self._days:
                cls = "off"
                label = "not available" 
                if self[day][slot]:
                    if overlay:
                        if overlay[day][slot]:
                            cls = "match"
                            label = "match!"
                        else:
                            cls = "nomatch"
                            label = "available"
                    else:
                        cls = "on"
                        label = "available!"

                out += "<td><div class='checkbox %s'><span>%s</span></div></td>" % (cls, label)
            out += "</tr>"
        out += "</table>"

        return out
        

class WeekgridField(models.CharField):
    description = Weekgrid.__doc__

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        # Override max_length to be sure it's long enough.
        kwargs['max_length'] = 127
        self.max_length = kwargs['max_length']
        super(WeekgridField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, Weekgrid):
            return value
        
        # If the field is empty, return an empty weekgrid.
        if len(value) == 0:
            return Weekgrid()

        data, slot_keys, day_keys = value.split(";")

        # Decompress slot_keys into tuple pairs.
        slot_strs = slot_keys.split(',')
        slots = []
        for slot_str in slot_strs:
            slots.append(tuple([float(slot_hr) for slot_hr in slot_str.split('-')]))

        # Decompress day_keys into day numbers.
        days = [int(day_str) for day_str in day_keys.split(',')]

        wg = Weekgrid(slots=slots, days=days)

        # Consume data string into weekgrid object.
        for slot in slots:
            for day in days:
                wg[day][slot] = (data[0] == "T")
                data = data[1:]

        return wg

    def get_prep_value(self, value):
        # Key data
        day_keys = ",".join(["%s" % day for day in value._days])
        slot_keys = ",".join(["%d-%d" % slot for slot in value._slots])

        # Actual data
        data = ""
        for slot in value._slots:
            for day in value._days:
                data += "T" if value[day][slot] else "F"

        return "%s;%s;%s" % (data,slot_keys,day_keys)

    def formfield(self, **kwargs):
        defaults = {'form_class': WeekgridFormField}
        defaults.update(kwargs)
        return super(WeekgridField, self).formfield(**defaults)

# Explain WeekgridFields to south
add_introspection_rules(
    [
        (
            [WeekgridField],
            [],
            {},
        ),
    ],
    ["^weekgrid\.WeekgridField"])

class WeekgridWidget(forms.MultiWidget):
    """
    A widget that displays a grid of checkboxes where the columns are days of the week and the rows are timeslots.
    """
    def __init__(self, attrs=None):
        
        # For now, get the days and slots from the default Weekgrid object.
        # These should be externally configurable eventually.

        template_wg = Weekgrid()
        self.days = template_wg._days
        self.slots = template_wg._slots
        field_count = len(self.days) * len(self.slots)

        # A tuple of form elements. For now, 21 select elements (seven days, three timeslots).
        widgets = (
            (forms.Select(attrs=attrs, choices=((True, "Available"), (False, "Not Available"))),)*field_count
            )

        super(WeekgridWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        """Called by render() if value is not yet a list. Splits input value to each of the widgets."""
        if value:
            return value.to_list()
        else:
            # If there's no value, decompress an empty Weekgrid.
            return Weekgrid().to_list()

    def render(self, name, value, attrs=None):
        """Returns widget rendered as unicode HTML. decompress() is called by render() to turn the Weekgrid dictionary into a list."""
        # Access field values by index, ie. value[0], value[1]
        return super(WeekgridWidget, self).render(name, value, attrs)

    def format_output(self, rendered_widgets):
        out = "<table class='weekgrid_widget editable'><tr><th></th>"
        for day in self.days:
            out += "<th>%s</th>" % daynames[day]
        out += "</tr>"

        for slot in self.slots:
            out += "<tr><th class='slot'>%s<div class='times'>(%s)</div></th>" % (slotlabels[slot], slottimes[slot])
            for day in self.days:
                out += "<td>%s</td>" % rendered_widgets.pop(0)
            out += "</tr>"
        out += "</table>"

        return out

class WeekgridFormField(forms.CharField):
    widget = WeekgridWidget

    def clean(self, formdata, *args, **kwargs):
        """formdata is a list of booleans from the select widgets. We need to turn it into a weekgrid object."""
        bools = [val == "True" for val in formdata]
        return Weekgrid().from_list(bools)
