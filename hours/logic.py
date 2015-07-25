
from positions.models import Organisation
from models import TimeRecord
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain


def get_unconfirmed_hours(user, organisation_id=None):
    timerecords = []
    reptimerecords = []
    stafftimerecords = []

    if user.is_authenticated():
        try:

            # Only allow organisation record lookup if the current user is a staff member.
            if organisation_id and user.is_staff:
                organisation = Organisation.objects.get(pk=organisation_id)
                reptimerecords = TimeRecord.objects.filter(organisation=organisation).filter(reviewed__isnull=True)

            elif user.get_profile().is_representative:
                rprofile = user.get_profile().try_get_representative_profile()
                if rprofile:
                    organisation = rprofile.organisation
        
                    # Get all unreviewed time records.
                    reptimerecords = TimeRecord.objects.filter(organisation=organisation).filter(reviewed__isnull=True)
        except ObjectDoesNotExist:
            pass

        # Only add staff records if not looking up records for a specific organisation.
        if user.is_staff and not organisation_id:
            # Admin staff must review all records that are not logged against an organisation in the system
            stafftimerecords = TimeRecord.objects.filter(organisation__isnull=True).filter(reviewed__isnull=True)
        
    timerecords = list(chain(reptimerecords, stafftimerecords))

    return timerecords
