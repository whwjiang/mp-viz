import React, { useState } from 'react';
import UserForm from './UserForm.js';
import APIData from './APIData.js';
import './App.css';

import 'materialize-css/dist/css/materialize.min.css';

const initialState = {
    user0: '',
    user1: '',
    submitted: false
}

const App = () => {
    const [state, setState] = useState(initialState);

    const handleChange = users => {
        setState({...users, submitted: true});
    }

    return (
        <div className='container'>
            <div className='row center'>
                <h1 className='black-text'>mpviz</h1>
            </div>
            <div className='row'>
                <div className='col m12 s12'>
                    <UserForm change={handleChange} />
                </div>
            </div>
            {state.submitted &&
                <>
                    <APIData 
                        user0={state.user0} 
                        user1={state.user1}
                    />
                </>
            }
        </div>
    );
}

export default App;

