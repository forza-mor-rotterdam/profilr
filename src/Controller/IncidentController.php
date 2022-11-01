<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class IncidentController extends AbstractController
{
    #[Route('/incident', name: 'app_incident')]
    public function index(): Response
    {
        return $this->render('incident/index.html.twig', [
            'controller_name' => 'IncidentController',
        ]);
    }
    #[Route('/incident/{id}', name: 'app_incident')]
    public function detail($id): Response
    {
        return $this->render('incident/detail.html.twig', [
            'id' => $id
        ]);
    }
}
