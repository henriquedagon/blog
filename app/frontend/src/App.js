// React imports
import React from 'react';
import './App.css';
// import axios from 'axios'
// Components
import Header from './components/Header/Header'
import Post from './components/Post/Post'
import LoginModal from './components/LoginModal/LoginModal'
import AddPost from './components/AddPost/AddPost'
// Other imports
import blue_screen from './components/Post/blue_screen.jpg'

class App extends React.Component {

    // initial state
    state = {
        posts: [
            // {'id': 1, image: freedom, imageName: 'freedom', text: 'uma parada'},
            // {'id': 2, image: freedom, imageName: 'freedom', text: 'outra parada'}
        ],
        showLoginModal: false,
        authToken: ''
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

    //   Toggle modal when Login is clicked
    toggleLoginModal = () => {
        const currentLoginState = this.state.showLoginModal
        this.setState({showLoginModal: !currentLoginState})
    }

    login = (token) => {
        this.setState({authToken: token})
        this.toggleLoginModal()
        console.log('token from app:',this.state.authToken)
    }

    render(){

        let modal = null
        if (this.state.showLoginModal){
            modal = (
                <LoginModal 
                    removeModal={this.toggleLoginModal}
                    setToken={this.login.bind(this)}
                    // login={this.loginHandler}    
                />
            )
        }

        return (
        <div>
            <Header loginClick={this.toggleLoginModal}/> 
            <AddPost/>
            {   //return all posts
                this.state.posts.map((post) => {
                    return <Post
                                image={post.image}
                                imageName={post.imageName}
                                title={post.title}
                                text={post.text}
                            />
                })
            }
            {modal}
        </div>
      
        );
    }
}

export default App;