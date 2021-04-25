import React from 'react';
import PropTypes from 'prop-types'

import './App.css';

const UserView = ({ user }) => {
    return (
        <>
        <div className="center">
            <img 
                src={user.avatar_url} 
                alt="user's avatar" 
                className="avatar"
            />
        </div>
        <br></br>
        <div className="center">
            <a 
                className='center black-text' 
                href={user.url}>
                    <b>{user.name}</b>
            </a>
        </div>
        <div className="center">
            <li>Ticks: {user.tick.length}</li>
            <li>To-dos: {user.todo.length}</li>
        </div>
        </>
    );
}

UserView.propTypes = {
    user: PropTypes.object.isRequired
}

export default UserView;