import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  constructor(private router: Router){}

  credentials = {
    email: '',
    name: '',
    uid: ''
  };

  ngOnInit(): void {
      if(localStorage.getItem('userdata') != undefined && localStorage.getItem('userdata') != null){
        this.router.navigate(['/']);
      }
    }
   
    onSubmit() {
      // Simulate login logic
      this.credentials['uid'] = this.generateUniqueId()
      console.log('Login credentials:', this.credentials);
      localStorage.setItem('userdata', JSON.stringify(this.credentials));
      //this.router.navigate(['/']);
      window.location.reload();
   
    }


  generateUniqueId(): string {
    const timestamp = Date.now().toString(36); // Convert current time to base-36
    const randomString = Math.random().toString(36).substring(2, 8); // Generate random base-36 string
    return `${timestamp}-${randomString}`;
  }

}
