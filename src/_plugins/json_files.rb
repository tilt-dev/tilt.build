class JsonFiles < Jekyll::Generator
  safe true
  class JsonFile < Jekyll::StaticFile
    def initialize(site, filename, json_data)
      super(site, nil, '.', filename, nil)
      @json_data = json_data
    end

    def write(dest)
      dest_path = destination(dest)
      FileUtils.mkdir_p(File.dirname(dest_path))
      File.open(dest_path, "wb") do |f|
        f.write(JSON.generate(@json_data))
      end
    end
  end

  def generate(site)
    (site.config["json_files"] || {}).each do |key, filename|
      json_data = key.split('.').inject(site.data) do |data, k|
        data[k] || {}
      end
      site.static_files << JsonFile.new(site, filename, json_data)
    end
  end
end
