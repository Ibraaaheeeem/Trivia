import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      viewMode:'GENERAL',
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: 0,
      searchQuery:''
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        if (result.questions == null) {
          this.setState({questions: []})
          alert("No questions found")
          if (result.categories == null) {
            alert("No categories found")
            return;
          }
          else{
            this.setState({
              viewMode:'GENERAL',
              totalQuestions: result.total_questions,
              categories: result.categories,
              //currentCategory: result.current_category,
            });    
          }
          return;
        }
        
        this.setState({
          viewMode:'GENERAL',
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          //currentCategory: result.current_category,
        });
        
        return;
      },
      error: function(xhr, status, error) {
        var err = JSON.parse(xhr.responseText)
        alert((err.message));
      },
    });
  };

  getCategories = () => {
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        if (result.categories == null) {
          alert("No category found");
          return;
        }
        
        this.setState({
          categories: result.categories,
        });
        
        return;
      },
      error: function(xhr, status, error) {
        var err = JSON.parse(xhr.responseText)
        alert((err.message));
      },
    });
  };

  
  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          viewMode:'CATEGORY',
          questions: result.questions,
          totalQuestions: result.totalQuestions,
          currentCategory: result.currentCategory,
        });
        return;
      },
      error: function(xhr, status, error) {
        var err = JSON.parse(xhr.responseText)
        alert((err.message));
      },
    });
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions/search`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          viewMode:'SEARCH',
          questions: result.questions,
          totalQuestions: result.total_questions,
          search_categories:result.categories,
          searchQuery:searchTerm,
          currentCategory:'SEARCH RESULT'
        });
        return;
      },
      error: function(xhr, status, error) {
        var err = JSON.parse(xhr.responseText)
        alert((err.message));
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            
              if (this.state.viewMode == 'GENERAL') this.getQuestions();
              else if (this.state.viewMode == 'CATEGORY') this.getByCategory(this.state.currentCategory)
              else if (this.state.viewMode == 'SEARCH') this.submitSearch(this.state.searchQuery)
            
            //alert(this.state.currentCategory)
            //this.getQuestions();
          },
          error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText)
            alert((err.message));
          },
        });
      }
    }
  };
  createNewCategory = ()=>{
    var name = window.prompt("Please, name your new category: ");
    if (name == null || name.trim() == '') return
    //var logo = window.prompt("Please, link to your category logo: ");
    $.ajax({
      url: '/categories', //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        new_category_name: name,
      }),
      
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        alert("Category created successfully")
        this.getCategories();
        return;
      },
      error: function(xhr, status, error) {
        var err = JSON.parse(xhr.responseText)
        alert((err.message));
      },
    });
  }

  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {Object.keys(this.state.categories).map((id) => (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
              >
                {this.state.categories[id]}
                <img
                  className='category'
                  alt={`${this.state.categories[id]}`}
                  src={`${this.state.categories[id]}.svg`}
                />
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch} />
          <h3 align='center' onClick={() => {
              this.createNewCategory();
            }}
          >
            Add New Category
          </h3>
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={q.category}
              categoryName = {this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
