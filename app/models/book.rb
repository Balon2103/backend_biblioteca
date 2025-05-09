class Book < ApplicationRecord
  validates :title, presence: true
  validates :author, presence: true
  validates :isbn, presence: true, uniqueness: true
  validates :quantity, presence: true, numericality: { greater_than_or_equal_to: 0 }
  
  # Categorías predefinidas
  CATEGORIES = [
    'Ficción',
    'No Ficción',
    'Ciencia',
    'Historia',
    'Biografía',
    'Tecnología',
    'Arte',
    'Filosofía',
    'Literatura',
    'Educación'
  ].freeze

  # Búsqueda por diferentes criterios
  def self.search(query)
    return all unless query.present?
    
    where(
      'title ILIKE :query OR 
       author ILIKE :query OR 
       isbn ILIKE :query OR 
       publisher ILIKE :query OR 
       category ILIKE :query',
      query: "%#{query}%"
    )
  end

  # Búsqueda por categoría específica
  def self.by_category(category)
    return all unless category.present?
    where(category: category)
  end
end 