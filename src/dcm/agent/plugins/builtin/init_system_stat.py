#
#  Copyright (C) 2014 Dell, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import dcm.agent.plugins.api.base as plugin_base
import dcm.agent.systemstats as systemstats


class InitSystemStat(plugin_base.Plugin):

    protocol_arguments = {
        "statType": ("The type of stat metric to initialize.", True,
                     str, None),
        "statName": ("The name of the new stat collector.", True, str, None),
        "holdCount": ("The number of stats to retain.", True, int, None),
        "checkInterval": ("The number of seconds over which to collect this "
                          "metric", True, float, None),
    }

    def __init__(self, conf, job_id, items_map, name, arguments):
        super(InitSystemStat, self).__init__(
            conf, job_id, items_map, name, arguments)

    def run(self):
        systemstats.start_new_system_stat(
            self.args.statName,
            self.args.statType,
            self.args.holdCount,
            self.args.checkInterval)
        return plugin_base.PluginReply(0, reply_type="void")


def load_plugin(conf, job_id, items_map, name, arguments):
    return InitSystemStat(conf, job_id, items_map, name, arguments)
