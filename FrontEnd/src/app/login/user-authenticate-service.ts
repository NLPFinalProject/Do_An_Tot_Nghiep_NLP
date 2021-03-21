import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
//import{User} from '@../../../src/app/login/User'

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

 SendEmail(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/SendMail`,user);
  }

  ActivateUser(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/activate`,user);
  }

  createUSer(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/`, user);
  }

  login(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/login`,user);
  }

  ForgotPassword(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/forgot-password`,user);
  }

  ResetPassword(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/reset-password`,user);
  }
  
}
