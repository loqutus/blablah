require 'shellwords'

PACKAGE_NAME = "blahblah"
PACKAGE_DESC = "blahblah"
PACKAGE_URL  = "git@github.com:loqutus/blablah.git"
PACKAGE_MNT  = "rusik@yandex-team.ru"
PACKAGE_DEPS = []

FILES        = ['share/**/vz*']
INSTALL_TO   = "/opt/blahblah"

desc "build .deb package"
task :package do
  max_mtime = (FILES + %w'Rakefile').map{ |f| File.mtime(f) }.max

  ver  = "0.0." + max_mtime.strftime("%Y%m%d.%H%M%S")

  cmd = [
    "fpm",
    "-a all",
    "-s dir",
    "-t deb",
    "-n #{PACKAGE_NAME}",
    "--description", Shellwords.shellescape(PACKAGE_DESC),
    "-v #{ver}",
    "-m #{PACKAGE_MNT}",
    "--vendor #{PACKAGE_MNT}",
    "--url #{PACKAGE_URL}",
    PACKAGE_DEPS.map{ |d| "-d #{d}" }.join(' '),
    FILES.map{ |f| "#{f}=#{File.join(INSTALL_TO,f)}" }.join(' ')
  ].join(' ')

  system cmd
  unless $?.success?
    STDERR.puts cmd
    STDERR.puts $!.inspect
    exit 1
  end
end
