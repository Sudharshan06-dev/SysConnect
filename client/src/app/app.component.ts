import {Component} from '@angular/core';
import {Router, RouterOutlet} from '@angular/router';
import {NgClass, NgIf} from '@angular/common';
import {HeaderComponent} from './layout/header/header.component';
import {SidebarComponent} from './layout/sidebar/sidebar.component';
import {LandingPageComponent} from './landing-page/landing-page.component';
import {NgxSpinnerComponent} from 'ngx-spinner';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NgClass, HeaderComponent, SidebarComponent, NgIf, LandingPageComponent, NgxSpinnerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  APP_TITLE = 'SysConnect'

  protected readonly spinnerTemplate = `<svg viewBox="0 0 100 50" width="120" height="60" xmlns="http://www.w3.org/2000/svg">
  <style>
    @keyframes float {
      0% { transform: translateY(0px); opacity: 0.3; }
      50% { transform: translateY(-5px); opacity: 1; }
      100% { transform: translateY(0px); opacity: 0.3; }
    }
    .molecule1 { animation: float 2s infinite ease-in-out; }
    .molecule2 { animation: float 2s infinite ease-in-out 0.4s; }
  </style>
  <!-- Left Structure -->
  <g class="molecule1" fill="orange" stroke="gray" stroke-width="1">
    <circle cx="20" cy="20" r="6"/>
    <circle cx="10" cy="30" r="6"/>
    <circle cx="30" cy="30" r="6"/>
    <line x1="20" y1="20" x2="10" y2="30" stroke-width="3"/>
    <line x1="20" y1="20" x2="30" y2="30" stroke-width="3"/>
  </g>
  <!-- Right Structure -->
  <g class="molecule2" fill="orange" stroke="gray" stroke-width="1">
    <circle cx="70" cy="15" r="7"/>
    <circle cx="60" cy="30" r="7"/>
    <circle cx="80" cy="30" r="7"/>
    <line x1="70" y1="15" x2="60" y2="30" stroke-width="4"/>
    <line x1="70" y1="15" x2="80" y2="30" stroke-width="4"/>
  </g>
</svg>`
  ;

  public isNonAuthPage = false
  public homePage = false

  drawerState = 'expanded';

  constructor(private route: Router) {
    this.route.events.subscribe(() => {
      this.isNonAuthPage = this.route.url.includes('/login') || this.route.url.includes('/registration')
      this.homePage = this.route.url.includes('/home')
    })
  }

  onDrawerStateChange(state: string): void {
    this.drawerState = state;
  }

}
