class BooksController < ApplicationController
  before_action :authenticate_user!
  before_action :set_book, only: [:show, :edit, :update, :destroy]

  def index
    @books = Book.all
    @books = @books.search(params[:search]) if params[:search].present?
    @books = @books.by_category(params[:category]) if params[:category].present?
    @categories = Book::CATEGORIES
  end

  def show
  end

  def new
    @book = Book.new
    @categories = Book::CATEGORIES
  end

  def edit
    @categories = Book::CATEGORIES
  end

  def create
    @book = Book.new(book_params)

    if @book.save
      redirect_to @book, notice: 'Libro creado exitosamente.'
    else
      @categories = Book::CATEGORIES
      render :new
    end
  end

  def update
    if @book.update(book_params)
      redirect_to @book, notice: 'Libro actualizado exitosamente.'
    else
      @categories = Book::CATEGORIES
      render :edit
    end
  end

  def destroy
    @book.destroy
    redirect_to books_url, notice: 'Libro eliminado exitosamente.'
  end

  private

  def set_book
    @book = Book.find(params[:id])
  end

  def book_params
    params.require(:book).permit(:title, :author, :isbn, :publisher, :publication_year, :description, :quantity, :category)
  end
end 