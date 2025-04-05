import {Component, EventEmitter, OnInit, Output, ViewChild} from '@angular/core';
import {
  DrawerComponent,
  DrawerContainerComponent,
  DrawerContentComponent,
  DrawerSelectEvent
} from '@progress/kendo-angular-layout';
import {Router, RouterOutlet} from '@angular/router';
import {
  bellIcon,
  inboxIcon,
  menuIcon,
  starOutlineIcon,
  logoutIcon,
  userIcon, SVGIcon
} from '@progress/kendo-svg-icons';
import {ButtonComponent} from '@progress/kendo-angular-buttons';
import {Location} from '@angular/common';
import {LocalStorageHelper} from '../../../services/local-storage.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [
    DrawerContainerComponent,
    DrawerComponent,
    RouterOutlet,
    DrawerContentComponent,
    ButtonComponent
  ],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent implements OnInit {

  public expanded = true;
  public mode: any = 'push'; // 'push', 'overlay', or 'squeeze'
  public mini = false;
  public width = 240;
  public selected = 'Dashboard';
  @ViewChild('drawer') public drawer!: DrawerComponent;
  @Output() drawerStateChange = new EventEmitter<string>();
  public menuSvg: SVGIcon = menuIcon;
  public applicantMenuItems = [
    {text: 'Application', route: '/application-enrollment', svgIcon: inboxIcon},
    {text: 'Profile', route: '/profile', svgIcon: userIcon},
    {text: 'Logout', route: '/logout', svgIcon: logoutIcon}
  ]

  public adminMenuItems = [
    {text: 'Dashboard', route: '/admin-dashboard', svgIcon: inboxIcon},
    {text: 'Courses', route: '/schedule-course', svgIcon: bellIcon},
    {text: 'Application', route: '/application-enrollment-details', svgIcon: starOutlineIcon},
    {text: 'Transcript', route: '/manage-transcripts', svgIcon: starOutlineIcon},
    {text: 'Profile', route: '/profile', svgIcon: userIcon},
    {text: 'Logout', route: '/logout', svgIcon: logoutIcon}
  ];

  public studentMenuItems = [
    {text: 'Courses', route: '/course-dashboard', svgIcon: bellIcon},
    {text: 'Transcript', route: '/request-transcript', svgIcon: starOutlineIcon},
    {text: 'Profile', route: '/profile', svgIcon: userIcon},
    {text: 'Logout', route: '/logout', svgIcon: logoutIcon}
  ];

  public professorMenuItems = [
    {text: 'Courses', route: '/course-dashboard', svgIcon: bellIcon},
    {text: 'Profile', route: '/profile', svgIcon: userIcon},
    {text: 'Logout', route: '/logout', svgIcon: logoutIcon}
  ];

  /*Text => Menu name, Icon => image path, route: navigation*/
  public items: any = [];

  constructor(private route: Router, private location: Location, private localStorage: LocalStorageHelper) {
    let userRole = this.localStorage.getItem('user_details')?.role

    if (userRole == 'ADMIN') {
      this.items = this.adminMenuItems
    } else if (userRole == 'PROFESSOR') {
      this.items = this.professorMenuItems
    } else if (userRole == 'STUDENT') {
      this.items = this.studentMenuItems
    } else {
      this.items = this.applicantMenuItems
    }

  }

  ngOnInit() {
    this.items.map((item: any) => {
      if (item.route == this.location.path()) {
        item.selected = true
      }
    })
  }

  public onSelect(ev: DrawerSelectEvent): void {
    this.selected = ev.item.text;
    this.route.navigate([ev.item.route])
  }

  public onExpandChange(): void {
    this.expanded = !this.expanded
    this.drawer.toggle()
    const state = !this.expanded ? 'mini' : 'expanded';
    this.drawerStateChange.emit(state);
  }

}
