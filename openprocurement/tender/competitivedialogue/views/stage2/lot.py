# -*- coding: utf-8 -*-
from openprocurement.tender.competitivedialogue.models import STAGE_2_EU_TYPE, STAGE_2_UA_TYPE, STAGE2_STATUS
from openprocurement.api.utils import (
    opresource,
    json_view,
)
from openprocurement.api.models import get_now
from openprocurement.tender.openua.views.lot import TenderUaLotResource
from openprocurement.tender.openeu.views.lot import TenderEULotResource
from openprocurement.tender.openua.utils import calculate_business_date
from openprocurement.tender.openua.models import TENDERING_EXTRA_PERIOD


@opresource(name='Tender stage2 UA Lots',
            collection_path='/tenders/{tender_id}/lots',
            path='/tenders/{tender_id}/lots/{lot_id}',
            procurementMethodType=STAGE_2_UA_TYPE,
            description="Tender stage2 UA lots")
class TenderStage2UALotResource(TenderUaLotResource):

    @json_view(content_type="application/json", permission='edit_tender')
    def collection_post(self):
        """Add a lot
        """
        self.request.errors.add('body', 'data', 'Can\'t create lot for tender stage2')
        self.request.errors.status = 403
        return

    @json_view(permission='edit_tender')
    def delete(self):
        """Lot deleting
        """
        self.request.errors.add('body', 'data', 'Can\'t delete lot for tender stage2')
        self.request.errors.status = 403
        return

    def validate_update_tender(self, operation):
        tender = self.request.validated['tender']
        if tender.status not in ['active.tendering', STAGE2_STATUS]:
            self.request.errors.add('body', 'data',
                                    'Can\'t {} lot in current ({}) tender status'.format(operation, tender.status))
            self.request.errors.status = 403
            return
        if calculate_business_date(get_now(), TENDERING_EXTRA_PERIOD, tender) > tender.tenderPeriod.endDate:
            self.request.errors.add('body', 'data', 'tenderPeriod should be extended by {0.days} days'.format(
                TENDERING_EXTRA_PERIOD))
            self.request.errors.status = 403
            return
        return True


@opresource(name='Tender stage2 EU Lots',
            collection_path='/tenders/{tender_id}/lots',
            path='/tenders/{tender_id}/lots/{lot_id}',
            procurementMethodType=STAGE_2_EU_TYPE,
            description="Tender stage2 EU lots")
class TenderStage2EULotResource(TenderEULotResource):

    @json_view(content_type="application/json", permission='edit_tender')
    def collection_post(self):
        """Add a lot
        """
        self.request.errors.add('body', 'data', 'Can\'t create lot for tender stage2')
        self.request.errors.status = 403
        return

    @json_view(permission='edit_tender')
    def delete(self):
        """Lot deleting
        """
        self.request.errors.add('body', 'data', 'Can\'t delete lot for tender stage2')
        self.request.errors.status = 403
        return

    def validate_update_tender(self, operation):
        tender = self.request.validated['tender']
        if tender.status not in ['active.tendering', STAGE2_STATUS]:
            self.request.errors.add('body', 'data',
                                    'Can\'t {} lot in current ({}) tender status'.format(operation, tender.status))
            self.request.errors.status = 403
            return
        if calculate_business_date(get_now(), TENDERING_EXTRA_PERIOD, tender) > tender.tenderPeriod.endDate:
            self.request.errors.add('body', 'data', 'tenderPeriod should be extended by {0.days} days'.format(
                TENDERING_EXTRA_PERIOD))
            self.request.errors.status = 403
            return
        return True