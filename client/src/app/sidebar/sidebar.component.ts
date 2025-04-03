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
  calendarIcon,
  inboxIcon,
  menuIcon,
  starOutlineIcon,
  logoutIcon,
  userIcon, SVGIcon
} from '@progress/kendo-svg-icons';
import {ButtonComponent} from '@progress/kendo-angular-buttons';
import {Location} from '@angular/common';

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
export class SidebarComponent implements OnInit{

  public expanded = true;
  public mode : any = 'push'; // 'push', 'overlay', or 'squeeze'
  public mini = false;
  public width = 240;
  public selected = 'Dashboard';
  @ViewChild('drawer') public drawer!: DrawerComponent;
  @Output() drawerStateChange = new EventEmitter<string>();
  public menuSvg: SVGIcon = menuIcon;

  /*Text => Menu name, Icon => image path, route: navigation*/
  public items = [
    { text: 'Dashboard', route: '/student-details', svgIcon: inboxIcon },
    { text: 'Courses', route: '/schedule-course', svgIcon: bellIcon },
    { text: 'Assignments', route: '/class-registration',  svgIcon: starOutlineIcon },
    { text: 'Settings', route: '/settings', svgIcon: calendarIcon},
    { text: 'Profile', route: '/profile', svgIcon: userIcon},
    { text: 'Logout', route: '/logout', svgIcon: logoutIcon}
  ];

  constructor(private route: Router, private location: Location) {
  }

  ngOnInit() {
    this.items.map( (item: any) => {
      if(item.route == this.location.path()) {
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
