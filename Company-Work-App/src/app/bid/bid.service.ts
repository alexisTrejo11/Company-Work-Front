import { Injectable } from "@angular/core";
import { Bid, BidStatus } from "./bid.model";

@Injectable({"providedIn": "root"})
export class BidService {
    private bids: Bid[] = dummyBids;

    getBidById(id: number) {
        return this.bids.filter(bid => bid.id === id);
    }

    getActiveBids() {
        return this.bids;
    }   
}

const dummyBids: Bid[] = [
    {
      id: 1,
      code: "SEDATU-2024-0156",
      name: "Construcción de Unidad Básica de Rehabilitación (UBR) en Acapulco, Guerrero",
      description: "Construcción de edificio de 2 niveles con 850 m2 de construcción, incluye instalaciones médicas especializadas",
      status: BidStatus.PUBLISHED,
      openingDate: "15-03-2024",
      closingDate: "30-05-2024",
      budget: 18500000,
      documents: ["Términos de Referencia", "Plano Arquitectónico", "Estudio de Impacto Social"]
    },
    {
      id: 2,
      code: "SEMARNAT-2024-0892",
      name: "Rehabilitación de Red de Drenaje Pluvial en Tijuana, Baja California",
      description: "Rehabilitación de 5.8 km de red de drenaje pluvial en zona urbana, incluye reposición de pavimento",
      status: BidStatus.AWARDED,
      openingDate: "10-01-2024",
      closingDate: "15-03-2024",
      budget: 42750000,
      documents: ["Proyecto Ejecutivo", "Dictamen Técnico", "Manifestación de Impacto Ambiental"]
    },
    {
      id: 3,
      code: "SCT-2024-0341",
      name: "Modernización de Carretera Federal Cuernavaca - Taxco, Tramo II",
      description: "Ampliación a 4 carriles de 12.3 km, construcción de 3 pasos vehiculares y rehabilitación de estructura existente",
      status: BidStatus.AWARDED,
      openingDate: "05-02-2024",
      closingDate: "20-04-2024",
      budget: 1250000000,
      documents: ["Proyecto Ejecutivo", "Estudio de Tránsito", "Presupuesto Desglosado"]
    },
    {
      id: 4,
      code: "IMSS-2024-0678",
      name: "Equipamiento Médico para Hospital Regional en Monterrey",
      description: "Suministro e instalación de equipos médicos para áreas de urgencias y quirófanos (12 equipos completos)",
      status: BidStatus.IN_PREPARATION,
      openingDate: "01-04-2024",
      closingDate: "15-06-2024",
      budget: 38700000,
      documents: ["Catálogo de Equipos", "Especificaciones Técnicas", "Plan de Entrega"]
    },
    {
      id: 5,
      code: "CONAGUA-2024-1123",
      name: "Reconstrucción de Sistema de Agua Potable en Jojutla, Morelos",
      description: "Reposición de 8.5 km de tubería, construcción de tanque de almacenamiento y planta de bombeo",
      status: BidStatus.AWARDED,
      openingDate: "20-05-2024",
      closingDate: "10-07-2024",
      budget: 63200000,
      documents: ["Estudio Hidráulico", "Croquis de Ubicación", "Programa de Ejecución"]
    }
];