import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private loginUrl = 'https://your-backend-api/login';
  private loggedIn = false; // Example: Replace with actual authentication logic
  private user:any;


  constructor(private http: HttpClient, private router: Router) { }

  login(credentials: { email: string; password: string }): Observable<any> {
    return this.http.post(this.loginUrl, credentials);
  }



  isAuthenticated(): boolean {
    if(localStorage.getItem('userdata') != undefined && localStorage.getItem('userdata') != null && localStorage.getItem('userdata') != ''){
      return true;

    }else{

      return false;

    }
    
  }

  getUser(){
   this.user= localStorage.getItem('userdata');
   console.warn('User data');
   console.warn(this.user);
   return JSON.parse(this.user);
  }

  logout(){
    localStorage.removeItem('userdata');
    this.router.navigate(['/login']);
  }


}
