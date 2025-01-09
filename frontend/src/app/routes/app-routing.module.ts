import { NgModule } from "@angular/core";
import { ChessBoardComponent } from "../modules/chess-board/chess-board.component";
import { ComputerModeComponent } from "../modules/computer-mode/computer-mode.component";
import { RouterModule, Routes } from "@angular/router";
import { LoginComponent } from "../login/login.component";
import { AuthGuard } from '../auth.guard';



const routes: Routes = [
    { path: "", component: ComputerModeComponent, title: "Noventiq Chess Game",canActivate: [AuthGuard] },
    { path: 'login', component: LoginComponent },
    // { path: "against-friend", component: ChessBoardComponent, title: "Play against friend", canActivate: [AuthGuard] },
    { path: "against-computer", component: ComputerModeComponent, title: "Noventiq Chess Game",canActivate: [AuthGuard] }

]

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }