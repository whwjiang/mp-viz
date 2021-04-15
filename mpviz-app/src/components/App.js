import React, { useState, useEffect } from 'react';
import UserForm from './UserForm.js';
import './App.css';

const initialState = {
    user0: '',
    user1: '',
    submitted: false
}

const App = () => {
    const [state, setState] = useState(initialState);

    const handleChange = users => {
        setState({...users, [submitted]: true});
    }

    return (
        <div className='container'>
            <div className='row center'>
                <h1 className='white-text'>mpviz</h1>
            </div>
            <div className='row'>
                <div className='col m12 s12'>
                    <UserForm change={handleChange} />
                </div>
            </div>
        </div>
    );
}

export default App;

