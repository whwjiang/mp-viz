import React, { useState } from 'react';
import PropTypes from 'prop-types'

const initialValues = {
    user0: '',
    user1: ''
}

const UserForm = ({ change }) => {
    const [state, setState] = useState(initialValues);

    const handleChange = e => {
        let { value, name } = e.target;
        setState({
            ...state,
            [name]: value
        })
    };

    const handleSubmit = () => {
        change(state);
        setState(initialValues);
    };

    return (
        <>
        <div className="row">
                <div className="col m6 s12">
                    <label htmlFor="user0">First User ID</label>
                    <input
                        id="user0"
                        name="user0"
                        type="text"
                        value={state.user0}
                        onChange={handleChange}
                    />
                </div>

                <div className="col m6 s12">
                    <label htmlFor="user1">Second User ID</label>
                    <input
                        id="user1"
                        name="user1"
                        type="text"
                        value={state.user1}
                        onChange={handleChange}
                    />
                </div>
            </div>
            <div className="center">
                <button
                    id="submit-button"
                    type="button"
                    disabled={state.user0 === '' 
                           || state.user1 === '' 
                           || state.user0 === state.user1 }
                    onClick={handleSubmit}
                >
                    Submit
                </button>
            </div>
        </>
    );
}

UserForm.propTypes = {
    change: PropTypes.func.isRequired
}

export default UserForm;