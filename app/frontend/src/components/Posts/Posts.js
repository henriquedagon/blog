import React, { Component } from 'react'
import Post from '../Post/Post'

import blue_screen from './blue_screen.jpg'

class Posts extends Component {
    constructor (props){
        super (props)
    }

    state = {
        posts: [
        ],
    }   
    // get posts
    componentDidMount() {
        fetch("http://localhost:5000/api/api/posts/")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        posts: result.data.map((res, index) => {
                            return {
                                id: index,
                                image: "http://localhost:5000/api/api/files/"+res.img_filename,
                                imageName: res.image_name,
                                title: res.title,
                                text: res.post
                            }
                        })
                    });
                },
                (error) => {
                    this.setState({
                        posts: [
                            {'id': 0, image: blue_screen, imageName: 'blue screen', text: 'deu kao'},
                        ],
                    })
                }
            )
        }

    
    render(){
        return (
            <div>
                {   //return all posts
                    this.state.posts.map((post) => 
                        <Post
                            image={post.image}
                            imageName={post.imageName}
                            title={post.title}
                            text={post.text}
                        />
                    )
                }
            </div>
        )    
    }
}

export default Posts
