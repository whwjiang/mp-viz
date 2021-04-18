import React, { useState, useEffect } from 'react';
import fetch from 'node-fetch';
import UserForm from './UserForm.js';
import './App.css';

function formatRequestUrl(user0, user1) {
    return `http://localhost:5000/api/q=${user0}+${user1}%all`;
}

async function query(user0, user1) {
    var requestUrl = formatRequestUrl(user0, user1);

    return await fetch(requestUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(r => r.json())
    .then(data => {
        //console.log('Success:', data);
        return data;
    })
    .catch((error) => {
        console.error('Error: ', error);
    });

}

const initialState = {
    contents: {},
    loaded: false
}

const UserData = ({ user0, user1 }) => {
    const [state, setState] = useState(initialValues);

    useEffect(() => {
        query(user0, user1)
        .then(data => {
            setState({contents: data, loaded: true})
            console.log(data)
        })
    }, []);

    return (
        <div className='container'>
            {state.loaded ? ( <>
                <div className='center white-text'>
                    {state.user0}, {state.user1}
                </div> 
            </> ) : ( <>
                <div className='center white-text'>
                    Loading
                </div> 
            </> )}
        </div>
    );
}

export default UserData



