import pandas as pd
from .models import Invoice, Customer, File
from django.db import transaction

class FileParser:
    def __init__(self, upload):
        self.upload = upload
        self.clear_results()

    def __get_header(self):
        header = ['ContactName', 'InvoiceNumber', 'InvoiceDate', 'DueDate', 'Description', 'Quantity', 'UnitAmount']
        return header

    def __parse_header(self):
        try:
            self.clear_results()
            file_data = pd.read_csv(self.upload.file.path, nrows=1).columns
            print('file_data', file_data)
            header_rows = self.__get_header()
            for row in header_rows:
                if row not in file_data:
                    message = u'{row} missing in header'.format(row=row)
                    self.add_error('header', message, 0)
            if len(self.errors) > 0:
                return False
            else:
                return True
        except Exception as ex:
            return

    def parse(self):
        if self.__parse_header():
            file_data = pd.read_csv(self.upload.file.path, sep=",")
            row_iter = file_data.iterrows()
            for index, row in row_iter:
                if not pd.isna(row['ContactName']) and not pd.isna(row['InvoiceNumber']) \
                        and not pd.isna(row['InvoiceDate']) and not pd.isna(row['DueDate']) \
                        and not pd.isna(row['Description']) and not pd.isna(row['Quantity']) \
                        and not pd.isna(row['UnitAmount']):
                    customer, _ = Customer.objects.get_or_create(name=row['ContactName'])
                    objs = [
                        Invoice(

                            file=self.upload,
                            customer=customer,
                            number=row['InvoiceNumber'],
                            date=row['InvoiceDate'],
                            due_date=row['DueDate'],
                            description=row['Description'],
                            quantity=row['Quantity'],
                            unit_amount=row['UnitAmount']
                        )
                    ]
                    try:
                        with transaction.atomic():
                            Invoice.objects.bulk_create(objs)
                    except Exception as ex:
                        continue

            return True
        else:
            return False

    def clear_results(self):
        self.errors = []
        self.error_counts = {}
        self.total_errors = 0

    def add_error(self, value, message, line=None, name=None):
        counts = self.error_counts.get(value, 0)
        counts += 1
        self.total_errors += 1
        self.error_counts[value] = counts
        error = {'message': message, 'value': value}
        if line:
            error['line'] = line
        if name:
            error['name'] = name
        # logger.debug(u'FileParser:add_error - {} ({},{}).'.format(message, line, name))
        self.errors.append(error)
