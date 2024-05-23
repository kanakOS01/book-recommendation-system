from flask import Flask, jsonify, render_template, request
import pickle
import numpy as np

popular = pickle.load(open("data/popular.pkl", "rb"))
books = pickle.load(open("data/books.pkl", "rb"))
sim_score = pickle.load(open("data/sim_score.pkl", "rb"))
pivot_table = pickle.load(open("data/pivot_table.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    # return "Hello World"
    print(list(popular['Image-URL-L'].values)[0])
    return render_template("index.html",
                           book_image=list(popular["Image-URL-L"].values),
                           book_title=list(popular["Book-Title"].values),
                           book_author=list(popular["Book-Author"].values),
                           book_rating=list(popular["Mean-Rating"].values),
                           )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

# @app.route('/get_book_names')
# def get_book_names():
#     book_names = list(books.values)
#     response = jsonify({
#         'book_names': book_names
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response
    
@app.route('/get_recommendations', methods=['POST', 'GET'])
def get_recommendations():
    user_input = request.form.get('user-input').lower()
    response = []

    # Check if the book exists in the dataset
    if user_input in pivot_table.index.str.lower():
        book_idx = np.where(pivot_table.index.str.lower() == user_input)[0][0]
        distances = sim_score[book_idx]
        similar_books = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:5]
        for book in similar_books:
            book_info = []
            temp_df = books[books['Book-Title'].str.lower() == pivot_table.index[book[0]].lower()]
            book_info.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            book_info.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            book_info.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
            response.append(book_info)
    else:
        # Return an error message or redirect to a page indicating that the book was not found
        return "Book not found. Please try again."



    # print(response)
    return render_template('recommend.html', data=response)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/books_archive')
def books_archve():
    response = jsonify({
        'books': list(books['Book-Title'].drop_duplicates().values)
    })
    return response

if __name__ == "__main__":
    app.run(debug=True)
