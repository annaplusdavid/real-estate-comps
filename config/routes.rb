Rails.application.routes.draw do
  root 'comparables#index'

  get '/comparables/search', to: 'comparables#search'
end
