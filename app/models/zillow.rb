require 'json'

class Zillow
  # Rails.application.secrets.zillow_api_key
  def parameterize(params)
    URI.escape(params.collect{|k,v| "#{k}=#{v}"}.join('&'))
  end

  def self.search_results (address, city)
    params = {
      :address => address,
      :citystatezip => city
    }

    results = Rubillow::HomeValuation.search_results(params)

    if results.success?
      Rails.logger.info Hash.from_xml(results.xml).to_json
    end
    
    results
  end
end

