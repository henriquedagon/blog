import React from 'react';
import './AddPost.css'
import axios from 'axios'
import cors from 'cors'
axios.defaults.baseURL = 'http://localhost:5000/api/api'
axios.defaults.headers.common['token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTMyNjY1NDEsImlhdCI6MTU5MzE4MDE0MSwic3lzIjoiYmxvZyIsInVzciI6ImFkbWluaXN0cmFkb3IiLCJwc3ciOiIxMjM0NSIsImdycCI6IjIifQ._XJMTl8q5QcEZSB--VQN1qxwkw2Ah5uzjgsZb-NVRhE'
axios.defaults.headers.common['mode'] = 'no-cors'

class AddPost extends React.Component{
    constructor (props){
        super (props)

    }

    handleSubmit(event) {
        event.preventDefault();

        const form = document.getElementById('add-post-form')
        const data = new FormData(form)
        // data.append('title','titulo')
        // data.append('post','postagem')
        // data.append('categories','cat1,cat2')
        data.append('author','administrador')
        // data.append('token','eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTMyNjY1NDEsImlhdCI6MTU5MzE4MDE0MSwic3lzIjoiYmxvZyIsInVzciI6ImFkbWluaXN0cmFkb3IiLCJwc3ciOiIxMjM0NSIsImdycCI6IjIifQ._XJMTl8q5QcEZSB--VQN1qxwkw2Ah5uzjgsZb-NVRhE')
        const headers = new Headers({
            // 'token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTMyNjY1NDEsImlhdCI6MTU5MzE4MDE0MSwic3lzIjoiYmxvZyIsInVzciI6ImFkbWluaXN0cmFkb3IiLCJwc3ciOiIxMjM0NSIsImdycCI6IjIifQ._XJMTl8q5QcEZSB--VQN1qxwkw2Ah5uzjgsZb-NVRhE',
                                    //  'mode':'no-cors',
                                     'Access-Control-Allow-Origin':'*'})

        console.log('data:',data)
        const that = this
        // usar o axios
        // fetch(
        //     // 'https://jsonplaceholder.typicode.com/posts/'
        //     'http://localhost:5000/api/api/add_post/'
        // , {
        // method: 'POST',
        // body: data,
        // mode: 'no-cors',
        // headers: headers
        // })
        // .then(res => 
        //     // res.json()
        //     console.log(res))
        // // .then(
        // //     result => {
        // //         // that.props.setToken(result.token)
        // //         // console.log(that)
        // //         console.log('responsta:',result)
        // //     }
        // // )
        axios.post(
            'http://localhost:5000/api/api/add_post/'
            // 'https://jsonplaceholder.typicode.com/posts/'
            , data, {headers: headers})
            .then(response => console.log(response))

    }

    render(){
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
