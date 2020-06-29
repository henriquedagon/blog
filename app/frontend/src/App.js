// React imports
import React from 'react';
import './App.css';
// import axios from 'axios'
import { BrowserRouter } from 'react-router-dom'
import { Route } from 'react-router-dom'
// Components
import Header from './components/Header/Header'
import Post from './components/Post/Post'
import LoginModal from './components/LoginModal/LoginModal'
import AddPost from './components/AddPost/AddPost'
import Posts from './components/Posts/Posts'
// Other imports
import blue_screen from './components/Post/blue_screen.jpg'

class App extends React.Component {

    // initial state
    state = {
        // posts: [
        // ],
        loggedIn: false,
        showLoginModal: false,
        account: null,
        authToken: null,
    }


    //   Toggle modal when Login is clicked
    toggleLoginModal = () => {
        const currentLoginState = this.state.showLoginModal
        this.setState({showLoginModal: !currentLoginState})
    }

    login = (account, token) => {
        this.setState({
            account: account,
            authToken: token
        })
        this.toggleLoginModal()
        console.log('user:',this.state.account)
        console.log('token from app:',this.state.authToken)
    }

    render(){

        let modal = null
        if (this.state.showLoginModal){
            modal = (
                <LoginModal 
                    removeModal={this.toggleLoginModal}
                    login={this.login.bind(this)}
                />
            )
        }

        return (
        <BrowserRouter>
            <div>
                <Header 
                    loginClick={this.toggleLoginModal}
                    loggedIn={this.state.loggedIn}
                /> 

                {/* component value should be reference to class or function */}
                <Route path="/" exact component={Posts}/>

                <Route path="/add-post" exact component={() => 
                    <AddPost 
                        token={this.state.authToken}
                        account={this.state.account}/>
                } />

                {modal}

            </div>
        </BrowserRouter>
      
        );
    }
}

export default App;