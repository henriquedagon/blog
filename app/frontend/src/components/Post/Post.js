import React from 'react'
import './Post.css'

const post = (props) => {
    return (
        <div class="post">
            <img src={props.image} alt={props.imageName} class="post-image" />
            <h1 class="post-title">{props.title}</h1>
            <p class="post-text">{props.text}</p>
        </div>
    )
}

export default post
