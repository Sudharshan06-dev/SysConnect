import { Component } from '@angular/core';
import {
  CellTemplateDirective,
  ColumnComponent,
  DataBindingDirective,
  GridComponent
} from '@progress/kendo-angular-grid';
import {CompositeFilterDescriptor} from '@progress/kendo-data-query';
import {TabContentDirective, TabStripComponent, TabStripTabComponent} from '@progress/kendo-angular-layout';
import {label} from '../../../messages/label';


@Component({
  selector: 'app-application-enrollment-details',
  standalone: true,
  imports: [
    GridComponent,
    ColumnComponent,
    DataBindingDirective,
    TabStripComponent,
    TabStripTabComponent,
    TabContentDirective,
    CellTemplateDirective
  ],
  templateUrl: './applicant-details.component.html',
  styleUrl: './applicant-details.component.css'
})
export class ApplicantDetailsComponent {

  public labels = label.application_details

  public filter: CompositeFilterDescriptor = {
    logic: "and",
    filters: [],
  };

  public gridData = [
    {
      ReferenceNumber: "85AB671WE",
      FirstName: "Sudharshan",
      LastName: "Madhavan",
      Email: "sudharshan.madhavan1998@outlook.com",
      Username: "Sudharshan06",
      Role: "Student",
      Degree: "Masters",
      Major: "Software Engineering",
      Status: "Pending"
    },
    {
      ReferenceNumber: "01NC671AJ",
      FirstName: "Ratika",
      LastName: "Moolchandani",
      Email: "ratika@csu.fullerton.edu",
      Username: "Ratika",
      Role: "Professor",
      Degree: "Postdoctorate",
      Major: "Software Engineering",
      Status: "Pending"
    },
    {
      ReferenceNumber: "45XY999JK",
      FirstName: "Namrata",
      LastName: "Joshi",
      Email: "namjo@csu.edu",
      Username: "Namjo",
      Role: "Student",
      Degree: "Bachelors",
      Major: "Computer Science",
      Status: "Approved"
    },
    {
      ReferenceNumber: "12ZZ334KP",
      FirstName: "Emily",
      LastName: "Clark",
      Email: "emily@csu.edu",
      Username: "emilyC",
      Role: "Student",
      Degree: "Masters",
      Major: "Software Engineering",
      Status: "Rejected"
    }
  ];

// Tabs data (filtered)
  public pendingApplications: any
  public approvedApplications: any
  public rejectedApplications: any

  constructor() {
    this.approvedApplications = this.gridData.filter(app => app.Status === 'Approved');
    this.pendingApplications = this.gridData.filter(app => app.Status === 'Pending');
    this.rejectedApplications = this.gridData.filter(app => app.Status === 'Rejected');
  }

  public filterChange(filter: CompositeFilterDescriptor): void {
    this.filter = filter;
  }

  public approveApplication(applicantRecord: any) {
    console.log(applicantRecord);
    return
  }

  public rejectApplication(applicantRecord: any) {
    console.log(applicantRecord);
    return
  }
}
