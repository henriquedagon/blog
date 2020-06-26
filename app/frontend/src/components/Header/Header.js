import React from 'react';
import './Header.css'

const header = (props) => {
    return (
        <header class="main-header">
        <div>
            <a href="index.html" class="main-header__brand">
                SuperSim Blog
            </a>
        </div>
        <nav class="main-nav">
            <ul class="main-nav__items">
                <li class="main-nav__item">
                    <a onClick={props.loginClick}>Login</a>
                </li>
            </ul>
        </nav>
    </header>
    )
}

export default header
