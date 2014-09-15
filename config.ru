require 'rack-livereload'

use Rack::LiveReload, no_swf: true
use Rack::Static, urls: ["/bower_components"]
use Rack::Static, urls: [""], root: "public", index: "index.html"

index = lambda do |env|
  [404, { "Content-Type" => "text/html" }, "No page found"]
end
run(index)
