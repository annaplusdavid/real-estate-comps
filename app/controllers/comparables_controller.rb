class ComparablesController < ApplicationController

  def index
  end

  def search
    @address = search_params[:address]
    @city = search_params[:city]

    @results = Zillow.search_results(@address, @city)
    @comps = Zillow.z_comparables(@address, @city)
    
  end

  private
    def search_params
      params.permit(:address, :city)
    end
end
