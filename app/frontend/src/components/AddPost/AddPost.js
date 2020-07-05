import React from 'react';
import './AddPost.css'
import axios from 'axios'
import cors from 'cors'
import { Redirect } from 'react-router';
axios.defaults.baseURL = 'http://blog-api:5000/api/api'
axios.defaults.headers.common['mode'] = 'no-cors'

class AddPost extends React.Component{
    constructor (props){
        super (props)
    }

    state = {
        postAdded: false
    }

    handleSubmit(event) {
        event.preventDefault();

        const form = document.getElementById('add-post-form')
        const data = new FormData(form)
        data.append('author',this.props.account)
        
        axios.defaults.headers.common['token'] = this.props.token
        console.log('token:',this.props.token)
        axios.post('http://blog-api:5000/api/api/add_post/', data)
            .then(response => console.log(response))
        this.setState({postAdded:true})
    }

    render(){

        if (this.state.postAdded){
            return <Redirect to='/'/>
        }

        return (
            <form onSubmit={this.handleSubmit.bind(this)} id="add-post-form">
                <div class="form">
                    <div class="add-post-form" id="add-post">
                        <div class="form__content">
                            <label for="title">Title</label>
                            <input type="text" name="title" id="title" />
                            <br></br>
                            <label for="post">Post</label>
                            <input type="text" name="post" id="post" />
                            <br></br>
                            <label for="image">Image</label>
                            <input type="file" name="image" id="image" />
                            <br></br>
                            <label for="categories">Categories</label>
                            <input type="text" name="categories" id="categories" />
                        </div>
                        <div class="form__actions">
                            <button class="btn btn--passive">Cancel</button>
                            <button class="btn btn--success">Add post</button>
                        </div>
                    </div>
                </div>
            </form>
        )
    }
}
export default AddPost
