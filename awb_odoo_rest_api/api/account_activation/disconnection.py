from odoo import http
from odoo.http import request
from .authentication import OdooAPI 

import importlib
import json

Serializer = importlib.import_module(
    "odoo.addons.odoo-rest-api"
).controllers.serializers.Serializer

SUBSCRIPTION = "sale.subscription"

class OdooAPI(OdooAPI):

    @http.route('/api/activate-subs', type='json', auth='public', methods=["PUT"])
    # data = {"params": {"user_ids": [<id1>, <id2>, <id3>], "subs_status": "expired/exceed_usage"}}
    def _activate_users(self, **kwargs):
        user_ids = http.request.params
        if not user_ids:
            res = {
              "errors": [
                {
                  "status": 400,
                  "message": "Bad Request",
                  "code": 352,
                  "description": "required parameters: <user_ids>",
                  "links": {
                    "about": "http://www.domain.com/rest/errorcode/352"
                  },
                  "data": {},
                  "data_count": {},
                }
              ]
            }

            return json.dumps(res)

        records = request.env[SUBSCRIPTION].browse("code", "=", user_ids)

        # print(records, flush=True)
        # for record in records:
        #     record.write(
        #         {"subscription_status": "disconnection", "subscription_status_subtype": "disconnection-temporary"}
        #     )
        # records.env.cr.commit()

        # method for disconnecting users
        # return must be the processed records
        # if 2 out of 3 successful records
        # records must be set to 2 only
        # records = records.set_users_discon()

        # serializer = Serializer(records, "{id, name, partner_id}", many=True)
        # data = serializer.data
        res = {
            "success": [{
                "status": 200,
                "message": "User disconnection successful",
                "code": 200,
                "description": "",
                "data": records,
                # "data_count": len(data),
            }]
        }

        return res
