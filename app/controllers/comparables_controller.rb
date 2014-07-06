class ComparablesController < ApplicationController

  def index
  end

  def search
    @address = search_params[:address]
    
  end

  private
    def search_params
      params.permit(:address)
    end
end
