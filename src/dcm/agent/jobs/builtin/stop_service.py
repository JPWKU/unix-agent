#  ========= CONFIDENTIAL =========
#
#  Copyright (C) 2010-2014 Dell, Inc. - ALL RIGHTS RESERVED
#
#  ======================================================================
#   NOTICE: All information contained herein is, and remains the property
#   of Dell, Inc. The intellectual and technical concepts contained herein
#   are proprietary to Dell, Inc. and may be covered by U.S. and Foreign
#   Patents, patents in process, and are protected by trade secret or
#   copyright law. Dissemination of this information or reproduction of
#   this material is strictly forbidden unless prior written permission
#   is obtained from Dell, Inc.
#  ======================================================================
from dcm.agent import exceptions
import dcm.agent.jobs.direct_pass as direct_pass


class StopService(direct_pass.DirectPass):
    def __init__(self, conf, job_id, items_map, name, arguments):
        super(StopService, self).__init__(
            conf, job_id, items_map, name, arguments)

        try:
            self.cwd = self.conf.get_service_directory(arguments["serviceId"])
            self.ordered_param_list = [arguments["serviceId"]]
        except KeyError as ke:
            raise exceptions.AgentPluginConfigException(
                "The plugin %s requires the option %s" % (name, ke.message))


def load_plugin(conf, job_id, items_map, name, arguments):
    return StopService(conf, job_id, items_map, name, arguments)