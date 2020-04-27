# -*- coding: utf-8 -*-
import os
from freezegun import freeze_time
from tests.base.constants import DOCS_URL, AUCTIONS_URL
from tests.base.test import DumpsWebTestApp, MockWebTestMixin
from tests.base.data import tender_openeu, tender_openua
from openprocurement.tender.openua.tests.award import TenderAwardPendingResourceTestCase
from openprocurement.tender.openeu.tests.qualification import TenderQualificationBaseTestCase


TARGET_DIR = 'docs/source/tendering/basic-actions/http/'


class BaseResourceTest(MockWebTestMixin):
    AppClass = DumpsWebTestApp
    relative_to = os.path.dirname(__file__)
    docservice = True
    docservice_url = DOCS_URL
    auctions_url = AUCTIONS_URL

    def setUp(self):
        self.setUpMock()

        super(BaseResourceTest, self).setUp()
        if self.context_name == "qualification":
            response = self.app.get("/tenders/{}/qualifications".format(self.tender_id))
            self.assertEqual(response.content_type, "application/json")
            qualifications = response.json["data"]
            self.context_id = qualifications[0]["id"]
        else:
            self.context_id = self.award_id

    def tearDown(self):
        self.tearDownMock()
        super(BaseResourceTest, self).tearDown()

    def test_qualification_milestone(self):
        self.app.authorization = ('Basic', ('broker', ''))

        # valid creation
        request_data = {
            "code": "24h",
            "description": "One ring to bring them all and in the darkness bind them"
        }
        with open(TARGET_DIR + '24hours/{}-milestone-post.http'.format(self.context_name), 'w') as self.app.file_obj:
            with freeze_time("2020-05-02 02:00:00"):
                response = self.app.post_json(
                    "/tenders/{}/{}s/{}/milestones?acc_token={}".format(
                        self.tender_id, self.context_name, self.context_id, self.tender_token
                    ),
                    {"data": request_data},
                )
        self.assertEqual(response.status, "201 Created")

        if self.context_name != "award":
            return

        with freeze_time("2020-05-02 02:00:01"):
            with open(TARGET_DIR + '24hours/{}-patch.http'.format(self.context_name), 'w') as self.app.file_obj:
                self.app.patch_json(
                    "/tenders/{}/{}s/{}?acc_token={}".format(
                        self.tender_id, self.context_name, self.context_id, self.tender_token
                    ),
                    {"data": {"status": "active", "qualified": True, "eligible": True}},
                    status=403
                )

            # try upload documents
            response = self.app.get(
                "/tenders/{}/{}s/{}?acc_token={}".format(
                    self.tender_id, self.context_name, self.context_id, self.tender_token
                )
            )
            context = response.json["data"]
            bid_id = context.get("bid_id")
            bid_token = self.initial_bids_tokens[bid_id]

            with open(TARGET_DIR + '24hours/post-doc.http'.format(self.context_name), 'w') as self.app.file_obj:
                response = self.app.post_json(
                    "/tenders/{}/bids/{}/documents?acc_token={}".format(
                        self.tender_id, bid_id, bid_token),
                    {
                        "data": {
                            "title": u"укр.doc",
                            "url": self.generate_docservice_url(),
                            "hash": "md5:" + "0" * 32,
                            "format": "application/msword",
                        }
                    },
                    status=201
                )

            with open(TARGET_DIR + '24hours/put-doc.http'.format(self.context_name), 'w') as self.app.file_obj:
                self.app.put_json(
                    "/tenders/{}/bids/{}/documents/{}?acc_token={}".format(
                        self.tender_id, bid_id, response.json["data"]["id"], bid_token
                    ),
                    {
                        "data": {
                            "title": u"укр.doc",
                            "url": self.generate_docservice_url(),
                            "hash": "md5:" + "0" * 32,
                            "format": "application/msword",
                        }
                    },
                    status=200
                )


class TenderAwardMilestoneResourceTest(BaseResourceTest, TenderAwardPendingResourceTestCase):
    initial_data = tender_openua
    context_name = "award"


class TenderQualificationMilestoneResourceTest(BaseResourceTest, TenderQualificationBaseTestCase):
    initial_data = tender_openeu
    context_name = "qualification"
