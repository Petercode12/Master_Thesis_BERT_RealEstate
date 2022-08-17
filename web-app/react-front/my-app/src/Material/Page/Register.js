import { React, Component } from 'react'
import '../Style/Login.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';

const defaultState = {
    email: null,
    password: null,
    passwordConfirm: null,
    agreeService: 0,
    nameError: null,
    emailError: null,
    passwordError: null,
    passwordConfirmError: null,
    agreeServiceError: null,
    isLogIn: null,
}

class Register extends Component {
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
        let passwordConfirmError = "";
        let agreeServiceError = "";
        console.log(this.state.email, this.state.password, this.state.passwordConfirm, this.state.agreeService);

        const reg = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(.\w{2,3})+$/;
        if (!this.state.email || reg.test(this.state.email) === false) {
            emailError = "Email Field is Invalid ";
        }
        if (this.state.passwordConfirm !== this.state.password) {
            passwordConfirmError = "Wrong password";
        }
        if (!this.state.password) {
            passwordError = "Password field is required";
        }
        if (!this.state.passwordConfirm) {
            passwordConfirmError = "Password field is required";
        }
        if (this.state.agreeService === 0) {
            agreeServiceError = "Please check this box";
        }
        console.log(typeof (this.state.agreeService));

        if (emailError || passwordError || passwordConfirmError || agreeServiceError) {
            this.setState({ emailError, passwordError, passwordConfirmError, agreeServiceError });
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
            console.log("Wrong email password", this.state.agreeService);
        }
    }
    // componentDidMount() {

    //   fetch("http://localhost:8080/register", {
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
                    <div className="row g-0">
                        <div className="login d-flex align-items-center py-5">
                            <div className="container">
                                <div className="row">
                                    <div className="col-sm-10 col-md-6 col-lg-4 mx-auto wrap-box">
                                        <h4 className="login-heading mb-4 text-center fw-normal">Create Account</h4>

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
                                            <div className="form-floating mb-3">
                                                <input type="password" className={"form-control " + (this.state.passwordError ? 'invalid' : '')} id="floatingPassword1" name="passwordConfirm" placeholder="Confirm Password" value={this.state.passwordConfirm} onChange={this.handleInputChange} />
                                                <label htmlFor="floatingPassword" className="row-header">Confirm password</label>
                                                <span className="text-danger">{this.state.passwordConfirmError}</span>
                                            </div>
                                            <div className="form-check mb-3 fs-6">
                                                <input className="form-check-input" type="checkbox" id="agreeService" name="agreeService" value={1 - this.state.agreeService} onChange={this.handleInputChange} />
                                                <label className="form-check-label" for="agreeService">
                                                    Agree with <a href="#">Terms of service</a>
                                                </label>
                                                <br />
                                                <span className="text-danger">{this.state.agreeServiceError}</span>
                                            </div>

                                            <div className="d-grid">
                                                <button className="btn btn-lg btn-primary btn-login text-uppercase fw-bold mb-2" type="button" onClick={() => this.submit()}>Sign Up</button>

                                                <div className="text-center small">
                                                    Already have an account? <a href="/">Login</a>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
export default Register;