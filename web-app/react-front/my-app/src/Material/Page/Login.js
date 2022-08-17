import { React, Component } from 'react'
import '../Style/Login.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";
const defaultState = {
    email: null,
    password: null,
    nameError: null,
    emailError: null,
    passwordError: null,
    isLogIn: null,
}

class Login extends Component {
    constructor() {
        super();
        this.state = defaultState;
        this.handleInputChange = this.handleInputChange.bind(this);
    }
    handleInputChange(event) {
        const target = event.target;
        var value = target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });
    }
    validate() {
        let emailError = "";
        let passwordError = "";
        console.log(this.state.email, this.state.password);

        const reg = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(.\w{2,3})+$/;
        if (!this.state.email || reg.test(this.state.email) === false) {
            emailError = "Email Field is Invalid ";
        }
        if (!this.state.password) {
            passwordError = "Password field is required";
        }
        if (emailError || passwordError) {
            this.setState({ emailError, passwordError });
            return false;
        }
        return true;
    }

    submit() {
        if (this.validate()) {
            this.setState({ isLogIn: true });
            console.warn(this.state);
            //this.setState(defaultState);

        }
        else {
            console.log("Wrong email password");
        }
    }
    // componentDidMount() {

    //   fetch("http://localhost:8080/login", {
    //     method: "POST",
    //     headers: {
    //       Accept: "application/json",
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({
    //       email: this.state.email,
    //       password: this.state.password,
    //     })
    //   })
    //     .then((res) => res.json())
    //     .then((json) => {
    //       this.setState({
    //         items: json,
    //         DataisLoaded: true
    //       });
    //     })

    // }
    render() {
        return (
            <div className="App" >
                <div className="container-fluid ps-md-0 bg-image">
                    <div class="row g-0">
                        <div className="login d-flex align-items-center py-5">
                            <div className="container">
                                <div className="row">
                                    <div className="col-sm-10 col-md-6 col-lg-4 mx-auto wrap-box">
                                        <h3 className="login-heading mb-4 text-center">Welcome back!</h3>

                                        <form>
                                            <div className="form-floating mb-3">
                                                <input type="email" className={"form-control " + (this.state.emailError ? 'invalid' : '')} id="floatingInput" name='email' placeholder="name@example.com" value={this.state.email} onChange={this.handleInputChange} />
                                                <label for="floatingInput" className="row-header">Email address</label>
                                                <span className="text-danger">{this.state.emailError}</span>
                                            </div>
                                            <div className="form-floating mb-3">
                                                <input type="password" className={"form-control " + (this.state.passwordError ? 'invalid' : '')} id="floatingPassword" name="password" placeholder="Password" value={this.state.password} onChange={this.handleInputChange} />
                                                <label htmlFor="floatingPassword" className="row-header">Password</label>
                                                <span className="text-danger">{this.state.passwordError}</span>
                                            </div>

                                            <div className="form-check mb-3">
                                                <input className="form-check-input" type="checkbox" value="" id="rememberPasswordCheck" />
                                                <label className="form-check-label" for="rememberPasswordCheck">
                                                    Remember password
                                                </label>
                                            </div>

                                            <div className="d-grid">
                                                <button className="btn btn-lg btn-primary btn-login text-uppercase fw-bold mb-2" type="button" onClick={() => this.submit()}>Sign in</button>
                                                <div className="text-center">
                                                    <a href="#" className="small">Forgot password?</a>
                                                </div>
                                                <div className="text-center small">
                                                    Don't have an account? <a href="#">Sign up</a>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div >

        )
    }
}
export default Login;