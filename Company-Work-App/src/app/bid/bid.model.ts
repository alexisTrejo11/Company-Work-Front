export interface Bid {
  id?: number;
  code: string;
  name: string;
  description: string;
  openingDate: string;
  closingDate: string;
  budget: number;
  status: BidStatus;
  documents: any; 
  contract?: Contract;
}

export enum BidStatus {
  IN_PREPARATION = "IN_PREPARATION",
  PUBLISHED = "PUBLISHED",
  AWARDED = "AWARDED",
  CANCELED = "CANCELED",
}

export enum ContractStatus {
  ACTIVE = "ACTIVE",
  SUSPENDED = "SUSPENDED",
  TERMINATED = "TERMINATED",
  BREACHED = "BREACHED",
}

export enum TaskStatus {
  PENDING = "PENDING",
  IN_PROGRESS = "IN_PROGRESS",
  COMPLETED = "COMPLETED",
  DELAYED = "DELAYED",
}

export enum UserRole {
  ADMIN = "ADMIN",
  SUPERVISOR = "SUPERVISOR",
  EMPLOYEE = "EMPLOYEE",
  CONTRACTOR = "CONTRACTOR",
}

export enum Priority {
  HIGH = "HIGH",
  MEDIUM = "MEDIUM",
  LOW = "LOW",
}


export interface Contract {
  id?: number;
  contractNumber: string;
  bid?: Bid;
  //contractor?: Company;
  startDate: string;
  endDate: string;
  amount: number;
  status: ContractStatus;
  //clauses: ContractClause[];
}