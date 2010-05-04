#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import adminfuncs
import summary
import detail
import citieswith

class Hello(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Hello from admin land")
        
def main():
    application = webapp.WSGIApplication([('/admin/', Hello),
                                          ('/admin/memcacheclear', adminfuncs.ClearCache),
                                          ('/admin/reload', adminfuncs.ReloadData),
                                          ('/admin/dataclear', adminfuncs.ClearData),
                                          ('/admin/DebugInfo', adminfuncs.DebugInfo)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
