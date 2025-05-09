class AddCategoryToBooks < ActiveRecord::Migration[7.1]
  def change
    add_column :books, :category, :string
  end
end 