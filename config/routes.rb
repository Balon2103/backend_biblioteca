Rails.application.routes.draw do
  devise_for :users
  
  root 'books#index'
  
  resources :books
  resources :loans, only: [:index, :create, :update]
  
  namespace :admin do
    resources :users
    resources :books
    resources :loans
  end
end 