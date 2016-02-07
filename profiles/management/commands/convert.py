from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):

    def handle(self, database="default", *args, **options):

        cursor = connections[database].cursor()

        cursor.execute("SHOW TABLE STATUS");

        for row in cursor.fetchall():
            if row[1] != "InnoDB":
                print "Converting %s" % row[0],
                result = cursor.execute("ALTER TABLE %s ENGINE=INNODB" % row[0])
                print result