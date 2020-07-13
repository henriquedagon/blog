import React from 'react';
import './LoginModal.css'
// import axios from 'axios'
import fernet from 'fernet/fernetBrowser'
import { Redirect } from 'react-router';

class loginModal extends React.Component{
    constructor (props){
        super (props)

    }
        
    state = {
        loggedIn: this.props.loggedIn
    }    

    handleSubmit(event) {
        event.preventDefault();

        var secret = new fernet.Secret("42j6K8yHSZQZO5DodraJpmh54MSw5AJ_6INhKB1ehmM=")

        var fernetToken = new fernet.Token({
            secret: secret,
            time: Date.parse(1),
            iv: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        })
        fernetToken.encode(JSON.stringify({
              "sys": "blog", 
              "usr": event.target.account.value, 
              "psw": event.target.password.value, 
              "grp": "2", 
              "tme": String(Date()).slice(0,25) 
        }))
        
        const account = event.target.account.value
        const that = this
        fetch('http://0.0.0.0:5000/api/api/get_token/'+fernetToken.token, {
          method: 'GET',
        }).then(res => res.json()).then(
            result => {
                if (result.token){
                    that.setState({loggedIn: true})
                    // console.log('that.state.loggedIn:',that.state.loggedIn)
                    that.props.login(account, result.token)            
                } else {
                    alert('Username or password incorrect')
                }
            }
        )
    }

    render() {

        const redirect = this.state.loggedIn

        // console.log('redirecting:',redirect)

        if (redirect) {
            return <Redirect to='/add-post'/>
        }

        return (
            <form onSubmit={this.handleSubmit.bind(this)} class="login-modal">
                <div id="backdrop" onClick={this.props.removeModal}></div>
                <div class="modal" id="login-modal">
                    <div class="modal__content">
                        <label for="account">Account</label>
                        <input type="text" name="account" id="account" />
                        <br></br>
                        <label for="password">Password</label>
                        <input type="password" name="password" id="password" />
                    </div>
                    <div class="modal__actions">
                        <button class="btn btn--passive" onClick={this.props.removeModal}>Cancel</button>
                        <button class="btn btn--success" onClick={this.loginHandler}>Login</button>
                    </div>
                </div>
            </form>
        )
    }
}

export default loginModal