# Copyright 2017 Jonathan Anderson
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

import dotenv
import os
import warnings

dotenv_path = dotenv.find_dotenv()
if dotenv_path == '':
    warnings.warn(
        'Unable to find a .env file, assuming environment-based configuration')

else:
    dotenv.load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError('no DATABASE_URL specified in .env or environment')
