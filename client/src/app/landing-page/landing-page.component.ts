import { Component } from '@angular/core';
import {ViewportScroller} from '@angular/common';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-landing-page',
  standalone: true,
  imports: [
    RouterLink
  ],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.css'
})
export class LandingPageComponent {

  constructor(private viewportScroller: ViewportScroller) {}

  scrollToSection(elementId: string): void {
    this.viewportScroller.scrollToAnchor(elementId);
  }

}
