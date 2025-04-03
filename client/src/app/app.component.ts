import { Component } from '@angular/core';
import {Router, RouterOutlet} from '@angular/router';
import {NgClass, NgIf} from '@angular/common';
import {HeaderComponent} from './header/header.component';
import {SidebarComponent} from './sidebar/sidebar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NgClass, HeaderComponent, SidebarComponent, NgIf],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'SysConnect';

  public isAuthPage = false

  drawerState = 'expanded';

  constructor(private route: Router) {
    this.route.events.subscribe(() => {
      this.isAuthPage = this.route.url.includes('/login') || this.route.url.includes('/registration')
    })
  }

  onDrawerStateChange(state: string): void {
    this.drawerState = state;
  }

}
