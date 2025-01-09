import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatToolbarModule } from "@angular/material/toolbar";
import { MatButtonModule } from "@angular/material/button"
import { RouterModule } from '@angular/router';
import { MatDialog, MatDialogModule } from "@angular/material/dialog";
import { PlayAgainstComputerDialogComponent } from '../play-against-computer-dialog/play-against-computer-dialog.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-nav-menu',
  templateUrl: './nav-menu.component.html',
  styleUrls: ['./nav-menu.component.css'],
  standalone: true,
  imports: [MatToolbarModule, MatButtonModule, RouterModule, MatDialogModule,CommonModule]
})
export class NavMenuComponent {
  
  user:any;
  username:string=''

  constructor(private dialog: MatDialog, private authService:AuthService) { }

  public playAgainstComputer(): void {
    this.dialog.open(PlayAgainstComputerDialogComponent);
  }

  ngOnInit(): void {
    console.log('ngOnInit: Component initialization logic here');
    this.user = this.authService.getUser();
    if(this.user != undefined){
      this.username = this.user['name'];
      console.warn(this.user['name']);
    }else{
      this.username = '';
      this.user =[]
    }
  }

  logout(){
    this.authService.logout();
    this.username = '';
      this.user =[]
  }


  

}
