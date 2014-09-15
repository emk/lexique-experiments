require 'rack-livereload'

use Rack::LiveReload, no_swf: true
use Rack::Static, urls: [""], root: "public", index: "index.html"

index = lambda do |env|
  [200, { "Content-Type" => "text/html" }, File.open("public/index.html")]
end
run(index)
