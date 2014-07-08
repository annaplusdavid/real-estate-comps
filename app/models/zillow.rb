require 'json'

class Zillow
  # Rails.application.secrets.zillow_api_key

  # ---------------------------------------------
  # Get zComps
  # http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA
  # ---------------------------------------------

  def self.z_comparables (address, city)
    z_comps = {}

    results = search_results(address, city)

    #if search result is successful, get the comparables (2 deep?)
    if results.success?
      obj = deep_comps(results.zpid, '25')

      #dropping score for now. Loop through top 25 results
      obj.comparables.each do |score, comp|
        z_comps[comp.zpid] = comp

        #for each of the top 25 get the next 3
        obj2 = deep_comps(comp.zpid, '3')

        obj2.comparables.each do |score2, comp2|
          z_comps[comp2.zpid] = comp2
        end
        #Rails.logger.info obj.comparables[key]
      end
    end
    z_comps
    # results
  end

  # ---------------------------------------------
  # Get Deep Search Results
  # http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA
  # ---------------------------------------------

  def self.search_results (address, city)
    params = {
      :address => address,
      :citystatezip => city
    }

    results = Rubillow::HomeValuation.search_results(params)

    # if results.success?
    #   Rails.logger.info Hash.from_xml(results.xml).to_json
    # end
    # results
  end


  # ---------------------------------------------
  # Get Comparables
  # http://www.zillow.com/webservice/GetDeepComps.htm?zws-id=<ZWSID<&zpid=48749425&count=5
  # ---------------------------------------------
  
  def self.comps (zpid, num)
    params = {
      :zpid => zpid,
      :count => num
    }

    results = Rubillow::HomeValuation.comps(params)

    # if results.success?
    #   Rails.logger.info Hash.from_xml(results.xml).to_json
    # end
    # results
  end

  # ---------------------------------------------
  # Get Deep Comparables
  # http://www.zillow.com/webservice/GetDeepComps.htm?zws-id=<ZWSID<&zpid=48749425&count=5
  # ---------------------------------------------
  
  def self.deep_comps (zpid, num)
    params = {
      :zpid => zpid,
      :count => num,
      :rentzestimate => 'true'
    }

    results = Rubillow::PropertyDetails.deep_comps(params)

    # if results.success?
    #   Rails.logger.info Hash.from_xml(results.xml).to_json
    # end
    # results
  end

  # ---------------------------------------------
  # Parse Search Result
  # ---------------------------------------------

end

