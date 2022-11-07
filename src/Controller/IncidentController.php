<?php

namespace App\Controller;

use Psr\Log\LoggerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Contracts\HttpClient\HttpClientInterface;
use Symfony\Contracts\HttpClient\ResponseInterface;

class IncidentController extends AbstractController
{
    #[Route('/incident', name: 'app_incident_index')]
    public function index(Request $request, RequestStack $requestStack, HttpClientInterface $apiClient, LoggerInterface $logger): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            $logger->warning('Not logged in', ['started' => $requestStack->getSession()->isStarted()]);
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        // $incidents = $apiClient->request('POST', 'https://diensten.rotterdam.nl/sbmob/api/msb/openmeldingen', [
        //     'query' => [],
        //     'body' => [
        //         'x' => 92441,
        //         'y' => 437718,
        //         'radius' => 200,
        //     ],
        //     'auth_bearer' => $requestStack->getSession()->get('msb_token')
        // ])->toArray()[results];
        $incidents = json_decode('[
              {
                "spoed": false,
                "datumMelding": "2021-09-10T18:58:56",
                "datumInbehandeling": null,
                "werkdagenSindsRegistratie": 296.0,
                "datumRappel": null,
                "herkomstCode": "BUR",
                "afdeling": {
                  "id": "204",
                  "omschrijving": "ZZZ_SO Verkeer & Vervoer"
                },
                "id": 4095249,
                "status": "Doorverwezen gekregen",
                "onderwerp": {
                  "id": "204",
                  "omschrijving": "Wegdek, voetpad of rijweg"
                },
                "omschrijving": null,
                "locatie": {
                  "adres": {
                    "straatNummer": "84948",
                    "straatNaam": "COUWENBURG",
                    "huisnummer": "108"
                  },
                  "x": 92404.05666,
                  "y": 437814.83599
                }
              },
              {
                "spoed": false,
                "datumMelding": "2022-10-31T13:53:19",
                "datumInbehandeling": null,
                "werkdagenSindsRegistratie": 6.0,
                "datumRappel": null,
                "herkomstCode": "BUR",
                "afdeling": {
                  "id": "239",
                  "omschrijving": "Wijkregie Centrum-Delfshaven "
                },
                "id": 4504557,
                "status": "Doorverwezen gekregen",
                "onderwerp": {
                  "id": "230",
                  "omschrijving": "Iets anders"
                },
                "omschrijving": null,
                "locatie": {
                  "adres": {
                    "straatNummer": "87408",
                    "straatNaam": "DELFTSESTRAAT",
                    "huisnummer": "5"
                  },
                  "x": 92363,
                  "y": 437858
                }
              },
              {
                "spoed": false,
                "datumMelding": "2022-11-02T09:31:50",
                "datumInbehandeling": null,
                "werkdagenSindsRegistratie": 4.0,
                "datumRappel": null,
                "herkomstCode": "BUR",
                "afdeling": {
                  "id": "111",
                  "omschrijving": "Schone Stad wijkreiniging Centrum"
                },
                "id": 4506344,
                "status": "Doorverwezen gekregen",
                "onderwerp": {
                  "id": "47",
                  "omschrijving": "zwerfvuil op straat"
                },
                "omschrijving": null,
                "locatie": {
                  "adres": {
                    "straatNummer": "87408",
                    "straatNaam": "DELFTSESTRAAT",
                    "huisnummer": "27"
                  },
                  "x": 92254.96999,
                  "y": 437777.95756
                }
              }]');

        $apiCalls = [];
        foreach ($incidents['results'] as $k => $incident) {
            $apiCalls[$k] = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/melding/' . $incident['id'], [
                'query' => [],
                'auth_bearer' => $requestStack->getSession()->get('msb_token')
            ]);
        }
        foreach ($apiCalls as $apiCall) {
            /** @var ResponseInterface $apiCall */
            $incidents['results']['_detail'] = $apiCall->toArray()['result'];
        }

        // render template
        return $this->render('incident/index.html.twig', [
            'incidents' => $incidents,
            'controller_name' => "My controller",
        ]);
    }

    #[Route('/incident/{id}', name: 'app_incident_detail')]
    public function detail(Request $request, int $id, RequestStack $requestStack, HttpClientInterface $apiClient): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        $incident = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/melding/' . $id, [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        // render template
        return $this->render('incident/detail.html.twig', [
            'id' => $id,
            'incident' => $incident
        ]);
    }

    #[Route('/incident/{id}/handle', name: 'app_incident_handle')]
    public function handle(Request $request, int $id, RequestStack $requestStack, HttpClientInterface $apiClient): Response
    {
        // if not logged in, redirect to login page
        if ($requestStack->getSession()->get('is_logged_in') !== true) {
            return $this->redirectToRoute('app_login_index');
        }

        // call api client
        $incident = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/melding/' . $id, [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        $groupedSubjects = $apiClient->request('GET', 'https://diensten.rotterdam.nl/sbmob/api/msb/onderwerpgroepen/', [
            'query' => [],
            'auth_bearer' => $requestStack->getSession()->get('msb_token')
        ])->toArray()['result'];

        // render template
        return $this->render('incident/handle.html.twig', [
            'id' => $id,
            'incident' => $incident,
            'groupedSubjects' => $groupedSubjects
        ]);
    }
}
